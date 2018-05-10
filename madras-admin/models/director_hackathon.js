'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('director_hackathon', {
    'name': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'director_hackathon',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.director_organization, {
      foreignKey: 'organization_id',
      
      as: '_organization_id',
    });
    
  };

  return Model;
};

