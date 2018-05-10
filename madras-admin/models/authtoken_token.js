'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('authtoken_token', {
    'key': {
      type: DataTypes.STRING,
      primaryKey: true 
    },
    'created': {
      type: DataTypes.DATE,
    },
  }, {
    tableName: 'authtoken_token',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.registration_applicant, {
      foreignKey: 'user_id',
      
      as: '_user_id',
    });
    
  };

  return Model;
};

