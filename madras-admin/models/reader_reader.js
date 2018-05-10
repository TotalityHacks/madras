'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('reader_reader', {
  }, {
    tableName: 'reader_reader',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.director_organization, {
      foreignKey: 'organization_id',
      
      as: '_organization_id',
    });
    
    Model.belongsTo(models.registration_applicant, {
      foreignKey: 'user_id',
      
      as: '_user_id',
    });
    
  };

  return Model;
};

